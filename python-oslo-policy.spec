%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.policy
%global pkg_name oslo-policy
%global with_doc 1
%global common_desc \
An OpenStack library for policy.

%global common_desc1 \
Test subpackage for the Oslo policy library.

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python3-%{pkg_name}}
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test dependencies
BuildRequires:  python3-hacking
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-context
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslotest
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-requests
BuildRequires:  python3-stevedore
BuildRequires:  python3-stestr
BuildRequires:  python3-sphinx
# Required to compile translation files
BuildRequires:  python3-babel

BuildRequires:  python3-requests-mock
BuildRequires:  python3-docutils
BuildRequires:  python3-PyYAML >= 3.1.0

Requires:       python3-requests
Requires:       python3-oslo-config >= 2:6.0.0
Requires:       python3-oslo-context >= 2.22.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-oslo-utils >= 3.40.0

Requires:       python3-yaml >= 5.1
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-oslo-i18n

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library
%{?python_provide:%python_provide python3-%{pkg_name}}

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-requests

Requires:  python3-requests-mock

%description -n python3-%{pkg_name}-tests
%{common_desc1}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo policy library

%description -n python-%{pkg_name}-lang
Translation files for Oslo policy library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f *requirements.txt

# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' oslo_policy/locale/*/LC_MESSAGES/*.po

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
# NOTE(jcapitao): we can re-enable warnings-as-failures once
# https://review.opendev.org/#/c/669427/ is in a tagged release
sphinx-build-3 -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_policy/locale --domain oslo_policy

%install
%{py3_install}
pushd %{buildroot}/%{_bindir}
for item in checker list-redundant policy-generator sample-generator
do
  # Create a versioned binary for backwards compatibility until everything is pure py3
  ln -s oslopolicy-$item %{buildroot}%{_bindir}/oslopolicy-$item-3
done
popd

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_policy/locale/*/LC_*/oslo_policy*po
rm -f %{buildroot}%{python3_sitelib}/oslo_policy/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_policy/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_policy --all-name

%check
export OS_TEST_PATH="./oslo_policy/tests"
PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslopolicy-policy-upgrade
%{_bindir}/oslopolicy-checker
%{_bindir}/oslopolicy-checker-3
%{_bindir}/oslopolicy-convert-json-to-yaml
%{_bindir}/oslopolicy-list-redundant
%{_bindir}/oslopolicy-list-redundant-3
%{_bindir}/oslopolicy-policy-generator
%{_bindir}/oslopolicy-policy-generator-3
%{_bindir}/oslopolicy-sample-generator
%{_bindir}/oslopolicy-sample-generator-3
%{_bindir}/oslopolicy-validator
%{python3_sitelib}/oslo_policy
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_policy/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-lang -f oslo_policy.lang
%license LICENSE

%changelog

