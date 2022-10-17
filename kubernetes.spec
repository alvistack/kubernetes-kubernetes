# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: kubernetes
Epoch: 100
Version: 1.23.13
Release: 1%{?dist}
Summary: Container Scheduling and Management
License: Apache-2.0
URL: https://github.com/kubernetes/kubernetes/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.17
BuildRequires: glibc-static
BuildRequires: rsync

%description
Kubernetes is a system for automating deployment, scaling, and
management of containerized applications. It groups containers that make
up an application into logical units for management and discovery.

%package kubectl
Summary: Kubernetes Command Line Tool

%description kubectl
The Kubernetes command line tool for interacting with the Kubernetes API.

%package kubelet
Summary: Kubernetes Node Agent
Requires: conntrack-tools
Requires: containernetworking-plugins
Requires: ebtables
Requires: ethtool
Requires: iproute
Requires: iptables >= 1.4.21
Requires: socat
Requires: util-linux >= 2.23.1

%description kubelet
The node agent of Kubernetes, the container cluster manager.

%package kubeadm
Summary: Kubernetes Cluster Bootstrapping Tool

%description kubeadm
The Kubernetes command line tool for bootstrapping a Kubernetes cluster.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
set -ex && \
    export KUBE_GIT_TREE_STATE="clean" && \
    export KUBE_GIT_COMMIT="592eca05be27f7d927d0b25cbb4241d75a9574bf" && \
    export KUBE_GIT_VERSION="v1.23.13" && \
    make WHAT="cmd/kubelet" && \
    make WHAT="cmd/kubeadm" && \
    make WHAT="cmd/kubectl"

%install
install -Dpm755 -d %{buildroot}%{_sysconfdir}/kubernetes/manifests
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_unitdir}
install -Dpm755 -d %{buildroot}%{_unitdir}/kubelet.service.d
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ _output/local/go/bin/kubeadm
install -Dpm755 -t %{buildroot}%{_bindir}/ _output/local/go/bin/kubectl
install -Dpm755 -t %{buildroot}%{_bindir}/ _output/local/go/bin/kubelet
install -Dpm644 -t %{buildroot}%{_unitdir}/ lib/systemd/system/kubelet.service
install -Dpm644 -t %{buildroot}%{_unitdir}/kubelet.service.d/ lib/systemd/system/kubelet.service.d/10-kubeadm.conf
./_output/local/go/bin/kubectl completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/kubectl
./_output/local/go/bin/kubeadm completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/kubeadm

%files kubectl
%license LICENSE
%{_bindir}/kubectl
%{_prefix}/share/bash-completion/completions/kubectl

%files kubelet
%license LICENSE
%dir %{_sysconfdir}/kubernetes
%dir %{_sysconfdir}/kubernetes/manifests
%{_bindir}/kubelet
%{_unitdir}/kubelet.service

%files kubeadm
%license LICENSE
%dir %{_unitdir}/kubelet.service.d
%{_bindir}/kubeadm
%{_unitdir}/kubelet.service.d/10-kubeadm.conf
%{_prefix}/share/bash-completion/completions/kubeadm

%changelog
